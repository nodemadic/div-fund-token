// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./DividendTokenERC20.sol";

contract TestDividendTokenERC20 is DividendTokenERC20 {
    constructor(string memory name_, string memory symbol_)
        DividendTokenERC20(name_, symbol_)
    {
        _mint(address(msg.sender), 100000);
    }
}
