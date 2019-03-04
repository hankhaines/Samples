function handleErrors(error, req, res, next) {
    res.status(400).send("You made a boo-boo Error: " + error.name);
};

module.exports = handleErrors;