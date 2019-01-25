from channels.consumer import SyncConsumer, AsyncConsumer


def hello(message):
    print("Hello, Channels!")  # long running task or printing


class PrintConsumer(SyncConsumer):
    def test_print(self, message):
        print("Test: " + message["text"])
