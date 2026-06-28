from sqlalchemy.orm import Session

from app.services.analysis_service import get_monthly_spending_summary
from app.services.budget_service import get_budget_status


def generate_coaching_message(db: Session, month: str) -> str:
    summary = get_monthly_spending_summary(db, month)
    budget = get_budget_status(db, month)
    lines = [f"{month} 소비 합계는 {summary['total_spent']:,}원입니다."]
    if budget["monthly_total_budget"]:
        lines.append(f"월 전체 예산 {budget['monthly_total_budget']:,}원 대비 사용률은 {budget['total_usage_rate']}%입니다.")
        if budget["total_remaining"] < 0:
            lines.append(f"전체 예산을 {-budget['total_remaining']:,}원 초과했습니다.")
        else:
            lines.append(f"남은 예산은 {budget['total_remaining']:,}원입니다.")
    if summary["top_categories"]:
        top_name, top_amount = summary["top_categories"][0]
        lines.append(f"가장 큰 지출 카테고리는 {top_name}이며 {top_amount:,}원을 사용했습니다.")
    over_budget = [item for item in budget["category_budgets"] if item["remaining_amount"] < 0]
    if over_budget:
        target = max(over_budget, key=lambda item: -item["remaining_amount"])
        lines.append(f"우선 {target['category']} 지출을 점검해 보세요. 카테고리 예산을 {-target['remaining_amount']:,}원 초과했습니다.")
    elif summary["top_categories"]:
        lines.append("가장 큰 지출 카테고리에서 주 1회만 소비를 줄여도 절약 효과를 빠르게 확인할 수 있습니다.")
    else:
        lines.append("아직 기록된 소비가 적습니다. 소비를 입력하면 더 구체적인 코칭을 제공할 수 있습니다.")
    return "\n".join(lines)
