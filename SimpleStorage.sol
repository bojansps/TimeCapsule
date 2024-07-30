// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // People public person = People({favoriteNumber: 2, name: "Patrick"});

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    uint256 public favoriteNumber;
    string myText;
    bool favoriteBool;

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }

    function storeText(string memory _myText) public {
        myText = _myText;
    }
    function retrieveText() public view returns(string memory) {
        return myText;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {

        people.push(People(_favoriteNumber,_name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    // function retrieve() public pure returns(uint256) {
    //    favoriteNumber + favoriteNumber
    //    return favoriteNumber;
    // }
}
