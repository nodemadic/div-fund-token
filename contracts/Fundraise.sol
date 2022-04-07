// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./DividendTokenERC20.sol";

contract Fundraise is DividendTokenERC20 {
    bool private _isMinted = false;
    address private _recipient;
    uint256 private _deadline;
    uint256 private _amountToRaise;

    constructor(
        address recipient_,
        string memory name_,
        string memory symbol_,
        uint256 hoursAvailable_,
        uint256 amountToRaise_
    ) DividendTokenERC20(10000, name_, symbol_) {
        _recipient = recipient_;
        _deadline = block.timestamp + (hoursAvailable_ * 1 hours);
        _amountToRaise = amountToRaise_;
    }

    mapping(address => uint256) public amountContributed;
    address[] public contributors;

    function closeRound() public {
        // Ensure that funding goal was not met
        require(_isMinted == false);

        // Check if deadline has passed
        require(block.timestamp >= _deadline);

        if (address(this).balance > _amountToRaise) {
            _mintForContributors();
        }
    }

    function _mintForContributors() private {
        for (uint256 i = 0; i < contributors.length; i++) {
            uint256 _tokensToMint = amountContributed[contributors[i]] *
                _tokensPerEth;
            _mint(contributors[i], _tokensToMint);
        }
    }

    uint256 private _tokensPerEth;

    function _calculateTokenMint() private {
        _tokensPerEth = 10000 / (address(this).balance);
    }

    function pledge(uint256 amount) public payable {
        // Check if in the fundraising period
        require(block.timestamp < _deadline);
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
