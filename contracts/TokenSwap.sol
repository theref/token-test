// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract BasicToken is ERC20 {
    uint8 internal _decimals;

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 decimals
    ) ERC20(_name, _symbol) {
        _decimals = decimals;
    }

    function decimals() public view virtual override returns (uint8) {
        return _decimals;
    }

    function faucet() public {
        _mint(msg.sender, 10000000);
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
        uint256 _GCD = _GCD(_tokenARatio, _tokenBRatio);
        TokenARatio = _tokenARatio / _GCD;
        TokenBRatio = _tokenBRatio / _GCD;
    }

    function _GCD(uint256 a, uint256 b) internal returns (uint256) {
        if (b == 0) {
            return a;
        }
        return _GCD(b, a % b);
    }

    function _AtoB(uint256 amount) internal view returns (uint256, uint256) {
        require(
            amount > TokenARatio,
            "Amount must be larger, the ratios don't work"
        );
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
