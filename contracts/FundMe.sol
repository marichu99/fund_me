// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
 //Application Binary Interface tell solodity what functions can be called on another contract
contract FundMe{
    
    // create a mapping from address to value
    mapping(address=>uint256) public addressToAmountFunded;
    address public owner ;
    address [] public funders;
    AggregatorV3Interface public priceFeed;
    constructor(address price_feed){       
        priceFeed=AggregatorV3Interface(price_feed); 
        owner=msg.sender;
    }
    function fund() public payable{
        uint256 minimumUSD=40*10**18;
        require(getConversionRate(msg.value)<=minimumUSD,"You need to spend more ETH");
       // initialise the mapping
        addressToAmountFunded[msg.sender]+=msg.value;
        funders.push(msg.sender);
    }
    function getVersion() public view returns(uint256){
        return priceFeed.version();
    }
    function getEntranceFee() public view returns(uint256){
        uint256 minimumUSD=40*10**18;
        uint256 price=getPrice();
        uint256 precision=1*10**18;
        return (minimumUSD * precision)/price;
    }
    function getPrice() public view returns(uint256){
        (
            ,
            int256 answer,
            ,
            , 
        ) = priceFeed.latestRoundData();
        return uint256(answer);
    }
    function getConversionRate(uint256 ethAmount) public view returns(uint256){
        uint256 ethPrice = getPrice();
        uint256 conversion = (ethAmount*ethPrice)/10**18;
        return conversion;
    }
    // modifiers are used to change the bahviours of functions in a declarative way
    modifier onlyOwner() {
        require(msg.sender==owner);
        _;
    }
     
    function withdraw()  payable onlyOwner public{
        // enable the sender to withdraw sent funds
        payable(msg.sender).transfer(address(this).balance);
        // using a for loop to set the funding amount to zero for all funders after withdrawal
        for(uint256 funderIndex=0;funderIndex<funders.length;funderIndex ++){
            address funder = funders[funderIndex];
            //set the value of the funder to zero using the addressToAmountFunded mapping
            addressToAmountFunded[funder]=0;
        }
        funders=new address[](0);
    }
}