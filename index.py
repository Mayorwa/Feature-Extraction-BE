from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import random

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/get-metrics')
async def root():
    return {'message': 'Metrics Retrieved successfully',
            'data': {"total_files_uploaded": 22, "total_patients_record": 340}}
