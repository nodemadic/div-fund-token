// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Fundraise.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/IERC721Receiver.sol";

contract Listings is IERC721Receiver {
    struct Listing {
        uint256 id;
        Fundraise fundraiseContract;
        address NFTaddress;
        uint256 tokenId;
        address NFTowner;
        bool active;
    }
    mapping(uint256 => Listing) public listings;
    uint256 public listingCount;

    // Should add an event to emit

    function onERC721Received(
        address _operator,
        address _from,
        uint256 _tokenId,
        bytes memory _data
    ) public override returns (bytes4) {
        return this.onERC721Received.selector;
    }

    function createListing(
        address _NFTaddress,
        uint256 _tokenId,
        address _recipient,
        string memory _name,
        string memory _symbol,
        uint256 _hoursToRaise,
        uint256 _amountToRaise
    ) public {
        ERC721(_NFTaddress).safeTransferFrom(
            msg.sender,
            address(this),
            _tokenId
        );
        Fundraise _fundraiseContract = new Fundraise(
            _recipient,
            _name,
            _symbol,
            _hoursToRaise,
            _amountToRaise
        );
        Listing memory listing = Listing(
            listingCount,
            _fundraiseContract,
            _NFTaddress,
            _tokenId,
            address(msg.sender),
            true
        );
        listings[listingCount] = listing;
        listingCount++;
    }

    function withdrawNFT(uint256 _listingId) public {
        Listing memory _listing = listings[_listingId];

        address _NFTowner = _listing.NFTowner;
        require(address(msg.sender) == _NFTowner);

        Fundraise _fundraiseContract = _listing.fundraiseContract;
        require(
            address(_fundraiseContract).balance <
                _fundraiseContract.amountToRaise()
        );

        uint256 _deadline = _fundraiseContract.deadline();
        require(block.timestamp > _deadline);

        address _NFTaddress = _listing.NFTaddress;
        uint256 _tokenId = _listing.tokenId;
        ERC721(_NFTaddress).safeTransferFrom(
            address(this),
            msg.sender,
            _tokenId
        );
    }

    function getListingDetails(uint256 _listingId)
        external
        view
        returns (Listing memory listing)
    {
        Listing memory _listing = listings[_listingId];
        return _listing;
    }
}
