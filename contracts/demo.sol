// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract foo {
    uint256 private _num1;

    constructor(uint256 num1_) {
        _num1 = num1_;
    }
}

contract bar is foo {
    uint256 private _num2;

    constructor(uint256 num1_, uint256 num2_) foo(num1_) {
        _num2 = num2_;
    }
}

contract baz is bar {
    uint256 private _num3;

    constructor(
        uint256 num1_,
        uint256 num2_,
        uint256 num3_
    ) bar(num1_, num2_) {
        _num3 = num3_;
    }
}
