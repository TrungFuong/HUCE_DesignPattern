// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/// @title TraceabilityContract
/// @notice Store and retrieve data hashes for batch traceability
contract TraceabilityContract {
    mapping(string => string) private hashes;

    event HashStored(string indexed batchId, string dataHash);

    function storeHash(string calldata batchId, string calldata dataHash) external {
        hashes[batchId] = dataHash;
        emit HashStored(batchId, dataHash);
    }

    function getHash(string calldata batchId) external view returns (string memory) {
        return hashes[batchId];
    }
}
