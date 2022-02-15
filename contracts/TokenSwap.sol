// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract BeerToken is ERC20 {
    constructor() public ERC20("Beer Token", "BEER") {
        _mint(msg.sender, 1000);
    }

    function getBeer() public {
        _mint(msg.sender, 100);
    }
}

contract CoffeeToken is ERC20 {
    constructor() public ERC20("Coffee Token", "COFF") {
        _mint(msg.sender, 1000);
    }

    function getCoffee() public {
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
        TokenARatio = _tokenARatio;
        TokenBRatio = _tokenBRatio;
        TokenA = IERC20(_tokenA);
        TokenB = IERC20(_tokenB);
    }

    function _AtoB(uint256 amount) internal view returns (uint256) {
        return (amount * TokenBRatio) / TokenARatio;
    }

    function _BtoA(uint256 amount) internal view returns (uint256) {
        return (amount * TokenARatio) / TokenBRatio;
    }

    function swapAforB(uint256 amount) public {
        uint256 BAmount = _AtoB(amount);
        uint256 allowance = TokenA.allowance(msg.sender, address(this));
        require(allowance >= amount, "Check the token allowance");
        TokenA.transferFrom(msg.sender, address(this), amount);
        TokenB.transfer(msg.sender, BAmount);
    }
}
