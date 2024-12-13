// ResultContract.sol
pragma solidity ^0.8.0;

contract ResultContract {
    mapping(address => string) public attendanceRecords;

    function recordAttendance(string memory rollNumber, string memory status) public {
        attendanceRecords[msg.sender] = status;
    }

    function getAttendance(address student) public view returns (string memory) {
        return attendanceRecords[student];
    }
}
