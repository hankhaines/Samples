'use strict';

import express from 'express';
const router = express.Router();

import {UserService} from "../src/services/UserService";

/* GET users listing. */
router.get('/', function(req, res, next) {
    var userService = new UserService();
    userService.findAllUsers().then( (user) => {
        res.send(user);
    }).catch(next);
});
module.exports = router;
