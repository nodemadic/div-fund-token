// SPDX-License-Identifier: GPL-3.0

pragma solidity <0.9.0;

contract DividendToken {
    // vars for constructor
    string public name;
    string public symbol;

    // remove decimals var if not allowing variable total supply
    uint8 public decimals = 18;
    uint256 public totalSupply = 100000 * (uint256(10)**decimals);

    constructor(string memory _name, string memory _symbol) {
        // constructor will later have to accept a hashmap of investors
        name = _name;
        symbol = _symbol;

        // will distrubute tokens out to hashmap of investors here
        balanceOf[msg.sender] = totalSupply;
        emit Transfer(address(0), msg.sender, totalSupply);
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

    // Quantity of tokens that a wallet has
    mapping(address => uint256) public balanceOf;

    // The scaled amount of ether credited to accounts per token but not yet
    // transferred those accounts

    // Withdrawls will decrease the amount stored in this variable
    mapping(address => uint256) public scaledDividendBalanceOf;

    // Cumulative amount of ether per token previously credited to account
    mapping(address => uint256) public scaledDividendCreditedTo;

    // Mapping of an account to a mapping of all of the accounts that are
    // allowed to make transfers from that account and for how much
    mapping(address => mapping(address => uint256)) public allowance;

    // Sets a wallet address's fields to up to date values
    // Called before any transfer
    function update(address account) internal {
        // Calculate scaled amount owed to wallet address
        uint256 owed = scaledDividendPerToken -
            scaledDividendCreditedTo[account];

        // Update the account's scaled dividend balance
        scaledDividendBalanceOf[account] += balanceOf[account] * owed;

        // Update the dividend amount that has been payed out to account
        scaledDividendCreditedTo[account] = scaledDividendPerToken;
    }

    function transfer(address to, uint256 value) public returns (bool success) {
        require(balanceOf[msg.sender] >= value);

        // Calculate and payout the dividends owed to both accounts before transfer
        update(msg.sender);
        update(to);

        // Adjust to and from balances for transfered amount
        balanceOf[msg.sender] -= value;
        balanceOf[to] += value;

        // Emit Transfer event for external logging and front end
        emit Transfer(msg.sender, to, value);

        // Retrun that transfer was successful
        return true;
    }

    function transferFrom(
        address from,
        address to,
        uint256 value
    ) public returns (bool success) {
        require(value <= balanceOf[from]);
        require(value <= allowance[from][msg.sender]);

        // Calculate and payout the dividends owed to both accounts before transfer
        update(from);
        update(to);

        // Adjust to and from balances for transfered amount
        balanceOf[from] -= value;
        balanceOf[to] += value;

        // Emit Transfer event for external logging and front end
        emit Transfer(from, to, value);

        // Retrun that transfer was successful
        return true;
    }

    function deposit() public payable {
        // Scale deposit then add the previous remainder
        uint256 available = (msg.value * scaling) + scaledRemainder;

        // Take the above total and divide it by the total number of tokens
        // Calculates how much each token is owed
        scaledDividendPerToken += available / totalSupply;

        // Compute new remainder
        scaledRemainder = available % totalSupply;
    }

    function withdraw() public {
        // Calculate and payout the dividends owed to account
        update(msg.sender);

        // Calculates how much is able to be withdrawn
        uint256 amount = scaledDividendBalanceOf[msg.sender] / scaling;

        // Retains the remainder for future withdrawls
        // Prevents permanent loss of funds from rounding issues
        scaledDividendBalanceOf[msg.sender] %= scaling;

        // Transfers the amound owed to the wallet
        payable(msg.sender).transfer(amount);
    }

    function approve(address spender, uint256 value)
        public
        returns (bool success)
    {
        allowance[msg.sender][spender] = value;
        emit Approval(msg.sender, spender, value);
        return true;
    }

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(
        address indexed owner,
        address indexed spender,
        uint256 value
    );
}
