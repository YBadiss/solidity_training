# Solidity Training

Some simple code to test my understanding during solidity training classes.

# op_code_runner

I was trying to figure out why the op code output of Remix looks so weird.
The goal of op_code_runner is to test some basic code changes, while
validatating that the output memory is the same.
It also tries to check gas usage change for each implementation.

## Usage

Change the `example.py` file to match your initial memory (stack + slots),
and the command sets you want to try out.

Then run
```shell
pipenv sync
pipenv run example
```

## Caveats

- The gas evaluation is super basic (read: wrong in a lot of cases)
- Only a few op codes are actually properly executed (only the ones I needed)

