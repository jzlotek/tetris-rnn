import tensorflow.keras as ks
import numpy as np

from piece import PIECE_FACTORIES

ls = ks.layers

batch_size = 32


def init_model(debug=False):
    board_input = ls.Input(shape=(batch_size, 20, 10, 1), name="board")
    aux_input = ls.Input(shape=(batch_size, 5,), name='aux')

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
        target_shape=(8, combined.shape[1]),
    )(combined)
    z = ls.LSTM(
        units=64,
        activation="relu",
        dropout=0.1,
        recurrent_dropout=0.1,
    )(z)
    z = ls.Reshape(
        target_shape=(4, z.shape[1]),
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

    model.compile(optimizer='adam', loss='mse')
    return model


def _zip_move_piece(move, piece):
    move.append(piece)
    return np.array(move)


def map_data(data):
    board = [np.array(tick.get("board")) for tick in data]
    aux = [_zip_move_piece(tick.get("last_move"), tick.get("next_piece")) for tick in data]
    next_move = [np.array(tick.get("current_move")) for tick in data]
    return (board, aux), next_move



def main():
    import json
    with open('joe_0608234605.json', 'r') as f:
        file = json.load(f)

    (board, aux), next_move = map_data(file)
    print(len(list(board)))
    print(len(list(aux)))
    print(len(list(next_move)))

    model = init_model(debug=True)
    model.fit(
        {"board": np.asarray(board), "aux": np.asarray(aux)},
        {"next_move": np.asarray(next_move)},
        batch_size=batch_size
    )
    model.save("model")


if __name__ == "__main__":
    main()
