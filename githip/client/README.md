This project was bootstrapped with [Create React App](https://github.com/facebookincubator/create-react-app).

You can find the most recent version of the guide [here](https://github.com/facebookincubator/create-react-app/blob/master/packages/react-scripts/template/README.md).

## Running the tests

```
cd githip/client/
yarn run test
```


## Running the app
First, ensure the server is running (check the root README for more info) then run:

```
npm start
```

or

```
yarn start
```

This will compile all the assets, watch for changes, and launch a browser at localhost:3000.


## Building for production / server
```
npm build
```

or

```
yarn build
```

This will compile and minimize all the files and put them in the build folder.
Not that the server is already setup to read from this folder, so if you simply go to
localhost:5000 it should just work.


### Notes on proxy
The package.json file in this folder is setup to `proxy` calls to localhost:5000.
If you want to run the server on a different port, you must change the `proxy` var to the proper address.
