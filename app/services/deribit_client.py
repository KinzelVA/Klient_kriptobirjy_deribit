from decimal import Decimal

import aiohttp


class DeribitClient:
    BASE_URL = "https://www.deribit.com/api/v2/public/get_index_price"

    async def get_index_price(self, ticker: str) -> Decimal:
        params = {"index_name": ticker}

        async with aiohttp.ClientSession() as session:
            async with session.get(self.BASE_URL, params=params, timeout=10) as response:
                response.raise_for_status()
                payload = await response.json()

        result = payload.get("result")
        if not result or "index_price" not in result:
            raise ValueError(f"Invalid response from Deribit for ticker={ticker}: {payload}")

        return Decimal(str(result["index_price"]))