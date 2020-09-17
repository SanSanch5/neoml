#include <common.h>
#pragma hdrstop

#include <NeoMathEngine/NeoMathEngineDefs.h>
#include <Timer.h>

std::map<std::string, CTimer::CTimerStruct> CTimer::Timers;
std::mutex CTimer::TimersGuard;

NEOMATHENGINE_API std::string PrintTimers() {
	return CTimer::PrintTimers();
}


