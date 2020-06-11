import tensorflow.keras as ks
import numpy as np

from piece import PIECE_FACTORIES

ls = ks.layers

batch_size = 32
STEPS = 4

def split_sequences(boards, aux, expected, steps):
    b, a, y = [], [], []
    for i in range(len(boards)):
        end_idx = i + steps

        if end_idx >= len(boards):
            break

        b.append(boards[i:end_idx])
        a.append(aux[i:end_idx])
        y.append(expected[end_idx])


    return np.array(b), np.array(a), np.array(y)


def init_model(debug=False):
    board_input = ls.Input(shape=(STEPS, 20, 10), name="board")
    aux_input = ls.Input(shape=(STEPS, 5,), name='aux')

    # Board state
    x = ls.Conv2D(
        filters=24,
        kernel_size=4,
        padding="same",
        activation="sigmoid",
    )(board_input)
    x = ls.MaxPooling2D(
        pool_size=(2, 2),
        strides=1,
    )(x)
    x = ls.Flatten()(x)
    x = ks.Model(inputs=board_input, outputs=x)

    # Next piece + input info
    y = ls.Dense(
        units=18,
    )(aux_input)
    y = ls.Flatten()(y)
    y = ks.Model(inputs=aux_input, outputs=y)

    # All input combined
    combined = ls.concatenate([x.output, y.output])
    # Combined model
    z = ls.Reshape(
        target_shape=(1, combined.shape[1]),
    )(combined)
    z = ls.LSTM(
        units=64,
        activation="relu",
        dropout=0.1,
        recurrent_dropout=0.1,
    )(z)
    z = ls.Reshape(
        target_shape=(4, z.shape[1] // 4),
    )(z)
    z = ls.LSTM(
        units=32,
        activation="relu",
        dropout=0.1,
        recurrent_dropout=0.1,
    )(z)
    z = ls.Dense(
        units=16,
        activation="relu",
    )(z)
    z = ls.Dense(
        units=4,
        activation="sigmoid",
        name="next_move"
    )(z)

    model = ks.Model(inputs=[x.input, y.input], outputs=z)

    if debug:
        model.summary()
        # ks.utils.plot_model(model, to_file="./model.png")

    model.compile(optimizer=ks.optimizers.Adam(1e-2, 1e-6), loss='binary_crossentropy', metrics=[ks.metrics.BinaryAccuracy()])
    return model


def _zip_move_piece(move, piece):
    move.append(piece)
    return np.array(move)


def map_data(data):
    board = [np.array(tick.get("board")).astype(bool).astype(int) for tick in data]
    aux = [_zip_move_piece(tick.get("last_move"), tick.get("next_piece")) for tick in data]
    next_move = [np.array(tick.get("current_move")) for tick in data]
    return (board, aux), next_move


def main():
    import json
    with open('../clean_john.json', 'r') as f:
        file = json.load(f)

    (board, aux), next_move = map_data(file)
    board, aux, next_move = split_sequences(board, aux, next_move, STEPS)

    # model = init_model(debug=True)
    model = ks.models.load_model("model.h5")
    hist = model.fit(
        {"board": np.asarray(board), "aux": np.asarray(aux)},
        {"next_move": np.asarray(next_move)},
        batch_size=len(next_move),
        epochs=2**11
    )
    model.save("model.h5")
    print(hist)


if __name__ == "__main__":
    main()
