export class UserRepository {
    static findUsers(filter) {
        var users = [
            {name: 'Hank Haines'},
            {name: 'Suzie Haines'},
            {name: 'Ashley Haines'}
        ];
        return new Promise( (resolve, reject) => {
            if (Math.random() * 100 < 50) resolve(users);
            else
                throw new Error("This is not handled properly");
        });
    }
}