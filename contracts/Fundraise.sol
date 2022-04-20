// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./DividendTokenERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Fundraise is DividendTokenERC20, Ownable {
    bool public isMinted = false;
    address public recipient;
    uint256 public deadline;
    uint256 public amountToRaise;
    uint256 public maxAmountToRaise;

    constructor(
        address recipient_,
        string memory name_,
        string memory symbol_,
        uint256 hoursToRaise_,
        uint256 amountToRaise_
    ) DividendTokenERC20(name_, symbol_) {
        recipient = recipient_;
        deadline = block.timestamp + (hoursToRaise_ * 1 hours);
        amountToRaise = amountToRaise_;
        // Change this multiplier with further testing
        maxAmountToRaise = (amountToRaise * 5) / 4;
    }

    // Shows amount of ETH given to this contract by wallet address
    mapping(address => uint256) public amountContributed;

    // Array of contributors to iterate through when round closes
    address[] public contributors;

    function closeRound() public onlyOwner {
        // Ensure that token wasn't already minted
        require(isMinted == false);

        require(address(this).balance >= amountToRaise);

        // // Check if deadline has passed
        // require(block.timestamp >= _deadline);

        // Change flag to not be able to call certain functions
        // Calculate ratio of tokens distributed to ETH sent
        // Mint appropriate number of tokens minus contract fee
        // Send recipient (escrow contract likely?) their ETH

        isMinted = true;
        _calculateTokenMint();
        _mintForContributors();
        payable(recipient).transfer(amountToRaise);
        // Leftover ETH can be sent back to token buyers in the
        // form of a dividend
    }

    // Calculated within calcTokenMint function
    // Ratio of tokens to mint per ETH contributed
    uint256 private _tokensPerEth;

    // Not full 100000 because contract owner takes 0.25% of any raise
    function _calculateTokenMint() private {
        _tokensPerEth = 99750000000000000000000 / (address(this).balance);
    }

    // Iterate over array of contributors and mint appropriate number
    // of tokens using the ratio calculated previously

    // Then mint the 0.25% for the contract owner
    function _mintForContributors() private {
        for (uint256 i = 0; i < contributors.length; i++) {
            uint256 _tokensToMint = (amountContributed[contributors[i]] *
                _tokensPerEth) / 1000000000000000000;
            _mint(contributors[i], _tokensToMint);
        }
        _mint(owner(), 100000 - totalSupply());
    }

    // Basic locking away funds for a set timeframe function
    // Adds user information to a map and array for minting later
    function pledge(uint256 _amount) public payable {
        // Check if amount they are sending was intended
        require(msg.value == _amount);

        // Check if pledging nonzero amount
        require(_amount > 0);

        // Check if in the fundraising period
        require(block.timestamp < deadline);

        // Check if round is already closed
        require(isMinted == false);

        // Check if already raised enough * multiplier
        require(_amount <= maxAmountToRaise);
        require(address(this).balance <= maxAmountToRaise);

        // If array doesnt contain pledger, add pledger to array
        if (amountContributed[msg.sender] == 0) {
            contributors.push(msg.sender);
        }

        // Update the mapping
        amountContributed[msg.sender] += _amount;
    }

    function getRefund() public {
        // Need to add more here to prevent exploit
        // Somebody could remove their funds here if they call
        // before funds are sent to seller

        // Ensure that funding goal was not met
        require(isMinted == false);

        // Check if deadline has passed
        require(block.timestamp >= deadline);

        uint256 amount = amountContributed[msg.sender];
        amountContributed[msg.sender] = 0;
        payable(msg.sender).transfer(amount);
    }
}
