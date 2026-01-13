"""
Logs API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from datetime import datetime, timedelta, timezone

from models.user import User
from utils.dependencies import get_current_admin_user
from services.log_analyzer import get_log_analyzer
from loguru import logger


router = APIRouter(prefix="/api/logs", tags=["logs"])


@router.get("/errors", response_model=dict)
async def get_error_summary(
    hours: int = Query(24, ge=1, le=168, description="Hours to analyze (1-168)"),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get error summary (Admin only)

    Returns error statistics for the specified time period
    """
    try:
        analyzer = get_log_analyzer()
        summary = analyzer.get_error_summary(hours=hours)
        return summary
    except Exception as e:
        logger.error(f"Failed to get error summary: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그 분석에 실패했습니다.",
        )


@router.get("/activity", response_model=dict)
async def get_activity_summary(
    hours: int = Query(24, ge=1, le=168, description="Hours to analyze (1-168)"),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get activity summary (Admin only)

    Returns activity statistics for the specified time period
    """
    try:
        analyzer = get_log_analyzer()
        summary = analyzer.get_activity_summary(hours=hours)
        return summary
    except Exception as e:
        logger.error(f"Failed to get activity summary: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그 분석에 실패했습니다.",
        )


@router.get("/api-stats", response_model=dict)
async def get_api_statistics(
    hours: int = Query(24, ge=1, le=168, description="Hours to analyze (1-168)"),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get API request statistics (Admin only)

    Returns API usage statistics for the specified time period
    """
    try:
        analyzer = get_log_analyzer()
        stats = analyzer.get_api_stats(hours=hours)
        return stats
    except Exception as e:
        logger.error(f"Failed to get API stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그 분석에 실패했습니다.",
        )


@router.get("/automation", response_model=dict)
async def get_automation_statistics(
    days: int = Query(7, ge=1, le=30, description="Days to analyze (1-30)"),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get automation statistics (Admin only)

    Returns blog and newsletter automation statistics
    """
    try:
        analyzer = get_log_analyzer()
        stats = analyzer.get_automation_stats(days=days)
        return stats
    except Exception as e:
        logger.error(f"Failed to get automation stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그 분석에 실패했습니다.",
        )


@router.get("/recent", response_model=dict)
async def get_recent_logs(
    level: Optional[str] = Query(None, description="Filter by level (INFO, WARNING, ERROR)"),
    hours: int = Query(1, ge=1, le=24, description="Hours to fetch (1-24)"),
    limit: int = Query(100, ge=10, le=1000, description="Max entries to return"),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get recent logs (Admin only)

    Returns recent log entries
    """
    try:
        analyzer = get_log_analyzer()
        start_time = datetime.now(timezone.utc) - timedelta(hours=hours)

        entries = analyzer.read_logs(
            start_time=start_time,
            level=level,
            limit=limit
        )

        return {
            "period": f"Last {hours} hour(s)",
            "filter": level or "ALL",
            "count": len(entries),
            "logs": [entry.to_dict() for entry in entries],
        }
    except Exception as e:
        logger.error(f"Failed to get recent logs: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="로그 조회에 실패했습니다.",
        )


@router.get("/dashboard", response_model=dict)
async def get_dashboard_stats(
    current_user: User = Depends(get_current_admin_user),
):
    """
    Get comprehensive dashboard statistics (Admin only)

    Returns all statistics for admin dashboard
    """
    try:
        analyzer = get_log_analyzer()

        return {
            "errors_24h": analyzer.get_error_summary(hours=24),
            "activity_24h": analyzer.get_activity_summary(hours=24),
            "api_stats_24h": analyzer.get_api_stats(hours=24),
            "automation_7d": analyzer.get_automation_stats(days=7),
        }
    except Exception as e:
        logger.error(f"Failed to get dashboard stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="대시보드 통계 조회에 실패했습니다.",
        )
