// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract DividendTokenERC20 is ERC20 {
    constructor(
        uint256 initialSupply,
        string memory name_,
        string memory symbol_
    ) ERC20(name_, symbol_) {
        _mint(msg.sender, initialSupply);
    }

    // Amount to scale all fund calculations within contract by

    // This is to prevent permanent loss of funds from rounding issues
    uint256 public scaling = uint256(10)**8;

    // Holds remainder after calculating what divdend should be given to
    // each token after a deposit

    // Amount will be added to next dividend calculation upon future deposit
    uint256 public scaledRemainder = 0;

    // Total amount owed to each token since contract's inception from
    // each deposit

    // What is actually payable to a tokenholder will be calculated in other
    // locations within this contract
    uint256 public scaledDividendPerToken;

    // Withdrawls will decrease the amount stored in this variable
    mapping(address => uint256) public scaledDividendBalanceOf;

    // Cumulative amount of ether per token previously credited to account
    mapping(address => uint256) public scaledDividendCreditedTo;

    // Sets a wallet address's fields to up to date values
    // Called before any transfer
    function _update(address account) internal {
        // Calculate scaled amount owed to wallet address
        uint256 owed = scaledDividendPerToken -
            scaledDividendCreditedTo[account];

        // Update the account's scaled dividend balance
        scaledDividendBalanceOf[account] += balanceOf(account) * owed;

        // Update the dividend amount that has been payed out to account
        // New token holders will be shown to have already claimed previous
        // dividends
        scaledDividendCreditedTo[account] = scaledDividendPerToken;
    }

    function _beforeTokenTransfer(
        address from,
        address to,
        uint256 amount
    ) internal virtual override {
        _update(from);
        _update(to);
    }

    function deposit() public payable {
        // Scale deposit then add the previous remainder
        uint256 available = (msg.value * scaling) + scaledRemainder;

        // Take the above total and divide it by the total number of tokens
        // Calculates how much each token is owed
        scaledDividendPerToken += available / totalSupply();

        // Compute new remainder
        scaledRemainder = available % totalSupply();
    }

    function withdraw() public {
        // Calculate and payout the dividends owed to account
        _update(msg.sender);

        // Calculates how much is able to be withdrawn
        uint256 amount = scaledDividendBalanceOf[msg.sender] / scaling;

        // Retains the remainder for future withdrawls
        // Prevents permanent loss of funds from rounding issues
        scaledDividendBalanceOf[msg.sender] %= scaling;

        // Transfers the amound owed to the wallet
        payable(msg.sender).transfer(amount);
    }
}
