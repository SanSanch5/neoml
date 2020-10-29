#pragma once

#include <NeoML/NeoMLDefs.h>

#include <chrono>

using namespace std::chrono;

class CTimer {
public:
	CTimer( bool start = false ) : CTimer( "", "", start ) {}
	CTimer( const char* _name, CString _groupName = "", bool start = false );
	~CTimer();

	void Start();
	void Stop();

	float GetTimeInMs() const;

	static CString PrintTimers();

private:
	struct CTimerStruct {
		CTimerStruct() : delay( 0 ), count ( 0 ) {}

		nanoseconds delay;
		int64_t count;
		CString group;
	};

	CString name;
	CString groupName;
	system_clock::time_point startTime;
	nanoseconds timeDelay;
	int64_t count;
	bool isStarted;
	static CMap<CString, CTimerStruct> Timers;
	static CCriticalSection TimersGuard;
};

