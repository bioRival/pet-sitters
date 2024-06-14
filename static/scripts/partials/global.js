// Function to cut the string short adding ellipsis
function truncate(str, max) {
    return str.length > max ? str.substr(0, max-1) + '…' : str;
}