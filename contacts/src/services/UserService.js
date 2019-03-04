import {UserRepository} from "../repositories/UserRepository";

export class UserService {
    findAllUsers() {
        var users = UserRepository.findUsers([]);
        return users;
    }
}