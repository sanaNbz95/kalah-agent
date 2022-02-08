#!/usr/bin/env python3
import sys
import kgp

# Compare the difference of stones in my (north) store vs. the opponents store
# (south).  kgp.py always assumes the agent is on the south side of
# the board, to avoid confusion.

def evaluate(state):
    return state[kgp.SOUTH] - state[kgp.NORTH]


# shallowly evaluate the moves.
# the move with the best score is probably the best move to start search within.
def shallow_checker(state, side, move):
    after, _ = state.sow(side, move)
    return evaluate(after)


# alpha-beta pruning algorithm
def search(state, depth, alpha, beta, side, move):
    if depth == 0 or state.is_final():
        return (evaluate(state), move)

    moves = sorted(
        state.legal_moves(side),
        key=lambda x: shallow_checker(state, side, x),
        reverse=True,
    )

    if side == kgp.SOUTH:
        max_eval = (float("-inf"), None)
        for move in moves:
            after, again = state.sow(side, move)

            if again:
                return (search(after, depth, alpha, beta, side, move)[0], move)
            eval = search(after, depth - 1, alpha, beta, not side, move)[0]
            max_eval = max(max_eval, (eval, move), key=lambda x: x[0])
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = (float("inf"), None)
        for move in moves:
            after, again = state.sow(side, move)

            if again:
                return (search(after, depth, alpha, beta, side, move)[0], move)
            eval = search(after, depth - 1, alpha, beta, not side, move)[0]
            min_eval = min(min_eval, (eval, move), key=lambda x: x[0])
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


def agent(state):
    for depth in range(3, 12):
        yield search(state, depth, float("-inf"), float("inf"), kgp.SOUTH, None)[1]


# We can now use the generator function as an agent, as seen below.
#
# By default the client will connect to our training server, but you
# can change this by setting the "HOST" keyword:
#
#     kgp.connect(agent, host="localhost:2761")
#
# Note that by default kgp.py requires that the "websocket-client"
# library (not to be confused with "websockets", that ends with an
# "s") has to be installed for Python 3, as the public server is only
# accessible over a websocket connection.
#
# A more extensive example includes some agent metadata:
#
#     kgp.connect(agent, host    = "wss://kalah.kwarc.info/socket",
#                        token   = "A hopefully random string only I know",
#                        authors = ["Eva Lu Ator", "Ben Bitdiddle"],
#                        name    = "magenta")
#
# This will be sent to the server and used to identify a client over
# multiple connections.  You may leave out the TOKEN keyword, if you
# wish to stay anonymous, in which case your client will not appear in
# the leaderboard.

if __name__ == "__main__":
    host = sys.argv[1]
    port = sys.argv[2]

    kgp.connect(
        agent,
        name="Hunter",
        token="%^YgfrdFGVR4439okkBBVDSTYJJJJFS",
        authors=[
            "Sana Nabizadeh",
            "Mahshid Sahami",
            "Maryam Parvin",
            "Saleh Esmaeil Zadeh Soudijani",
        ],
        debug=True
        host=host,
        port=port
    )
