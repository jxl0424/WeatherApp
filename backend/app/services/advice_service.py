from app.integrations.nvidia_client import generate_advice
from app.schemas.weather import AdviceRequest, AdviceResponse


async def get_travel_advice(req: AdviceRequest) -> AdviceResponse:
    return await generate_advice(req)
