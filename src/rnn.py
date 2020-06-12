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
        if expected is not None:
            y.append(expected[end_idx])

    return \
        np.asarray(np.array(b)),\
        np.asarray(np.array(a)),\
        np.asarray(np.array(y))


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
    x = ls.Reshape(
        target_shape=(STEPS,x.shape[2]*x.shape[3])
    )(x)
    x = ks.Model(inputs=board_input, outputs=x)

    # Next piece + input info
    y = ls.Dense(
        units=18,
    )(aux_input)
    y = ks.Model(inputs=aux_input, outputs=y)

    # All input combined
    combined = ls.concatenate([x.output, y.output], axis=2)
    # Combined model
    z = ls.LSTM(
        units=64,
        activation="relu",
        dropout=0.1,
        recurrent_dropout=0.1,
        return_sequences=True,
    )(combined)
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
        name="next_move",
    )(z)

    model = ks.Model(inputs=[x.input, y.input], outputs=z)

    if debug:
        model.summary()
        # ks.utils.plot_model(model, to_file="./model.png")

    model.compile(
        optimizer=ks.optimizers.Adam(1e-2, 1e-6),
        loss='binary_crossentropy',
        metrics=[ks.metrics.BinaryAccuracy()])
    return model


def _zip_move_piece(move, piece):
    return np.array([*move,piece])


def map_data(data):
    board = [np.array(tick.get("board")).astype(bool).astype(int) for tick in data]
    aux = [_zip_move_piece(tick.get("last_move"), tick.get("next_piece")) for tick in data]
    next_move = [np.array(tick.get("current_move")) for tick in data]
    return (board, aux), next_move


def main():
    import json
    with open('default.json', 'r') as f:
        file = json.load(f)

    (board, aux), next_move = map_data(file)
    board, aux, next_move = split_sequences(board, aux, next_move, STEPS)

    model = init_model(debug=True)
    hist = model.fit(
        {"board": board, "aux": aux},
        {"next_move": next_move},
        batch_size=len(next_move),
        epochs=2**12
    )
    model.save("model.h5")

#    model = ks.models.load_model("models/joe_model.h5")
#    ks.utils.plot_model(model, to_file="./model.png")

#    total = 0
#    correct = 0
#    for i in range(len(board)):
#        b = board[i:i+1]
#        a = aux[i:i+1]
#        pred = model.predict(
#            {"board": b, "aux": a})[0]
#
#        nd = np.round(pred+0.2)
#        ex = next_move[i]
#        print(pred, nd, next_move[i])
#        if nd[0] == ex[0] and \
#                nd[1] == ex[1] and \
#                nd[2] == ex[2] and \
#                nd[3] == ex[3]:
#            correct += 1
#
#        total += 1
#    print(100*correct/total)


if __name__ == "__main__":
    main()
