class BlockchainTransactionBuilder:

    def __init__(self):
        self.transaction = {}

    def with_batch_id(self, batch_id: str):
        self.transaction["batch_id"] = batch_id
        return self

    def with_data_hash(self, data_hash: str):
        self.transaction["data_hash"] = data_hash
        return self

    def build(self):
        return self.transaction
