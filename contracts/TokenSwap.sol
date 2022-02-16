// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract BasicToken is ERC20 {
    constructor(string memory name, string memory symbol) ERC20(name, symbol) {}

    function faucet() public {
        _mint(msg.sender, 100);
    }
}

contract TokenSwap {
    uint256 public TokenARatio;
    uint256 public TokenBRatio;

    IERC20 public TokenA;
    IERC20 public TokenB;

    constructor(
        address _tokenA,
        address _tokenB,
        uint256 _tokenARatio,
        uint256 _tokenBRatio
    ) {
        TokenA = IERC20(_tokenA);
        TokenB = IERC20(_tokenB);
        TokenARatio = _tokenARatio;
        TokenBRatio = _tokenBRatio;
    }

    function _AtoB(uint256 amount) internal view returns (uint256, uint256) {
        uint256 useable = amount - (amount % TokenARatio);
        return ((useable * TokenBRatio) / TokenARatio, useable);
    }

    function swapAforB(uint256 amount) public {
        uint256 BAmount;
        uint256 useable;
        (BAmount, useable) = _AtoB(amount);
        uint256 allowance = TokenA.allowance(msg.sender, address(this));
        require(allowance >= useable, "Check the token allowance");
        TokenA.transferFrom(msg.sender, address(this), useable);
        TokenB.transfer(msg.sender, BAmount);
    }
}
