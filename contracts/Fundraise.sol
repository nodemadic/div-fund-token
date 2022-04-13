// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./DividendTokenERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Fundraise is DividendTokenERC20, Ownable {
    bool private _isMinted = false;
    address private _recipient;
    uint256 private _deadline;
    uint256 private _amountToRaise;
    uint256 private _maxAmountToRaise;

    constructor(
        address recipient_,
        string memory name_,
        string memory symbol_,
        uint256 hoursToRaise_,
        uint256 amountToRaise_
    ) DividendTokenERC20(name_, symbol_) {
        _recipient = recipient_;
        _deadline = block.timestamp + (hoursToRaise_ * 1 hours);
        _amountToRaise = amountToRaise_;
        // Change this multiplier with further testing
        _maxAmountToRaise = (_amountToRaise * 5) / 4;
    }

    // Shows amount of ETH given to this contract by wallet address
    mapping(address => uint256) public amountContributed;

    // Array of contributors to iterate through when round closes
    address[] public contributors;

    function closeRound() public onlyOwner {
        // Ensure that token wasn't already minted
        require(_isMinted == false);

        require(address(this).balance > _amountToRaise);

        // // Check if deadline has passed
        // require(block.timestamp >= _deadline);

        // Change flag to not be able to call certain functions
        // Calculate ratio of tokens distributed to ETH sent
        // Mint appropriate number of tokens minus contract fee
        // Send recipient (escrow contract likely?) their ETH

        _isMinted = true;
        _calculateTokenMint();
        _mintForContributors();
        payable(_recipient).transfer(_amountToRaise);
        // Leftover ETH can be sent back to token buyers in the
        // form of a dividend
    }

    // Calculated within calcTokenMint function
    // Ratio of tokens to mint per ETH contributed
    uint256 private _tokensPerEth;

    // Not full 10000 because contract owner takes 0.25% of any raise
    function _calculateTokenMint() private {
        _tokensPerEth = 99750000000000000000000 / (address(this).balance);
    }

    // Iterate over array of contributors and mint appropriate number
    // of tokens using the ratio calculated previously

    // Then mint the 0.25% for the contract owner
    function _mintForContributors() private {
        require(contributors[0] == msg.sender, "Value doesn't exist");
        for (uint256 i = 0; i < contributors.length; i++) {
            uint256 _tokensToMint = (amountContributed[contributors[i]] *
                _tokensPerEth) / 1000000000000000000;
            _mint(contributors[i], _tokensToMint);
        }
        _mint(owner(), 100000 - totalSupply());
    }

    // Basic locking away funds for a set timeframe function
    // Adds user information to a map and array for minting later
    function pledge(uint256 amount) public payable {
        // Check if in the fundraising period
        require(block.timestamp < _deadline);

        // Check if round is already closed
        require(_isMinted == false);

        // Check if already raised enough * multiplier
        // FIX THIS CHECK STATEMENT
        require(msg.value <= _maxAmountToRaise);

        // Check if amount they are sending was intended
        require(msg.value == amount);

        contributors.push(msg.sender);
        amountContributed[msg.sender] += amount;
    }

    function getRefund() public {
        // Need to add more here to prevent exploit
        // Somebody could remove their funds here if they call
        // before funds are sent to seller

        // Ensure that funding goal was not met
        require(_isMinted == false);

        // Check if deadline has passed
        require(block.timestamp >= _deadline);

        uint256 amount = amountContributed[msg.sender];
        amountContributed[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
