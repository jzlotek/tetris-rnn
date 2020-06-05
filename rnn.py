from keras import Sequential
from keras.layers import LSTM, LSTMCell, ConvLSTM2D, ConvLSTM2DCell, Input, Dropout, Dense, Embedding


def init_model():
    model = Sequential()
    # input_layer = Input(shape=(None,))
    model.add(Embedding(input_dim=200, output_dim=128))
    model.add(LSTM(256))
    model.add(Dense(4))
    model.summary()
    return model


if __name__ == "__main__":
    m = init_model()
