from __future__ import annotations

from pydantic import Field

from pp_food_runtime.models.common import FrozenModel
from pp_food_runtime.models.job import UserFacts


class CopyAllowlist(FrozenModel):
    product_name: str
    brand: str | None = None
    address: str | None = None
    price: str | None = None
    phone: str | None = None
    verified_hard_facts: dict[str, str] = Field(default_factory=dict)
    verified_soft_facts: list[str] = Field(default_factory=list)
    authorized_campaign_copy: list[str] = Field(default_factory=list)

    def exact_copy_lines(self) -> list[str]:
        values = [self.brand, self.product_name, *self.verified_soft_facts, self.address]
        values.extend(self.verified_hard_facts.values())
        values.extend(self.authorized_campaign_copy)
        return [value for value in values if value]


class CopyFirewall:
    def build(self, user_facts: UserFacts) -> CopyAllowlist:
        hard = dict(user_facts.verified_hard_facts)
        campaign = []
        if user_facts.default_copy_authorized:
            campaign = ["就是这一口"]
        return CopyAllowlist(
            product_name=user_facts.product_name,
            brand=user_facts.brand,
            address=user_facts.address,
            price=hard.get("price"),
            phone=hard.get("phone"),
            verified_hard_facts=hard,
            verified_soft_facts=user_facts.verified_soft_facts,
            authorized_campaign_copy=campaign,
        )
