import os
import uvicorn
from openenv.core import create_fastapi_app
from server.environment import PromptOptimizerEnvironment
from models import PromptOptimizerAction, PromptOptimizerObservation

app = create_fastapi_app(
    env=PromptOptimizerEnvironment,
    action_cls=PromptOptimizerAction,
    observation_cls=PromptOptimizerObservation,
)


def main():
    uvicorn.run(
        "server.app:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 7860)),
        workers=int(os.getenv("WORKERS", 4)),
    )


if __name__ == "__main__":
    main()
