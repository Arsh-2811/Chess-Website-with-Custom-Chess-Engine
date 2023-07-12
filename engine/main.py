from fastapi import FastAPI, APIRouter
from minimax import minimax
from fen import generate_new_fen
from pydantic import BaseModel

# ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
#                    "5": 3, "6": 2, "7": 1, "8": 0}
# filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3, 
#                    "e": 4, "f": 5, "g": 6, "h": 7}
# rowsToRanks = {v: k for k, v in ranksToRows.items()}
# colsToFiles = {v: k for k, v in filesToCols.items()} 

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware
# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your React Native app's origin
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

router = APIRouter()

class MoveRequest(BaseModel):
    fen: str
    depth: int

@app.post("/get-move")
def get_move(request: MoveRequest):
    fen = request.fen
    depth = request.depth

    white_to_move = True
    if fen.split()[1] == 'b':
        white_to_move = False

    evaluation, move = minimax(fen, depth, -1000000, 1000000, white_to_move)
    new_fen = generate_new_fen(fen, move)

    return new_fen

app.include_router(router)