import tensorflow.keras as ks
import numpy as np
from board import PIECES

ls = ks.layers


def init_model(debug=False):
    batch_size = 1
    board_input = ls.Input(shape=(batch_size, 20, 10), name="board")
    aux_input = ls.Input(shape=(batch_size, 5,), name='aux')

    # Board state
    x = ls.Conv2D(
        filters=24,
        kernel_size=3,
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
        name="predicted_move"
    )(z)

    model = ks.Model(inputs=[x.input, y.input], outputs=z)

    if debug:
        model.summary()
        # ks.utils.plot_model(model, to_file="./model.png")

    model.compile(optimizer='adam', loss='mse')
    return model

def get_next_piece(idx):
    piece = np.array(PIECES[idx - 1])
    h, w = piece.shape
    ret = np.zeros((2, 4))

    ret[:h, :w] = piece[:, :]

    return ret

def map_data(data):
    board = [np.array(tick.get("board")) for tick in data]
    next_piece = [get_next_piece(tick.get("next_piece")) for tick in data]
    last_move = [np.array(tick.get("last_move")) for tick in data]
    next_move = [np.array(tick.get("current_move")) for tick in data]
    return (board, next_piece, last_move), next_move



def main():
    import json
    with open('joe_0608234605.json', 'r') as f:
        file = json.load(f)

    (board, next_piece, last_move), next_move = map_data(file)

    model = init_model(debug=True)
    print(board[0])
    print(next_move[0])
    model.fit({"board": board}, {"predicted_move": next_move})


if __name__ == "__main__":
    main()
