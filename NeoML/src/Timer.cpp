#include <common.h>
#pragma hdrstop

#include <NeoML/Timer.h>

CMap<CString, CTimer::CTimerStruct> CTimer::Timers;
CCriticalSection CTimer::TimersGuard;

CString PrintNeoMLTimers() {
	return CTimer::PrintTimers();
}

CTimer::CTimer( const char* _name, CString _groupName, bool start ) :
	name( _name ), groupName( _groupName ), timeDelay( 0 ), count(0), isStarted( false )
{
	if( start ) {
		Start();
	}
}

CTimer::~CTimer()
{
	if( isStarted ) {
		Stop();
	}
	if( !name.IsEmpty() ) {
		const CCriticalSectionLock lock( TimersGuard );
		auto& timer = Timers.GetOrCreateValue( name );
		timer.delay += timeDelay;
		timer.count += count;
		timer.group = groupName;
	}
}

void CTimer::Start()
{
	assert( !isStarted );
	startTime = high_resolution_clock::now();
	isStarted = true;
}

void CTimer::Stop()
{
	assert( isStarted );
	auto stopTime = high_resolution_clock::now();
	timeDelay += duration_cast<nanoseconds>( stopTime - startTime );
	count++;
	isStarted = false;
}

float CTimer::GetTimeInMs() const
{
	auto currentTime = isStarted ? high_resolution_clock::now() - startTime : timeDelay;
	return currentTime.count() / 1e6;
}

CString CTimer::PrintTimers()
{
	if( Timers.IsEmpty() ) return "";

	const CCriticalSectionLock lock( TimersGuard );
	CString res;
	res += "\nGroup;Timer name;Total, ms;Avrg, ms;Count;%\n";

	TMapPosition pos = Timers.GetFirstPosition();
	while( pos != NotFound ) {

		auto& timerStruct = Timers.GetValue( pos );
		double delay = static_cast<double>( timerStruct.delay.count() ) / 1e6;
		// a head timer is a timer with the name equivalent to the group name
		auto groupHeadPos = Timers.GetFirstPosition( timerStruct.group );
		double delayFirstInGroup = static_cast<double>( 
			groupHeadPos == NotFound ? delay : Timers.GetValue( groupHeadPos ).delay.count() / 1e6 );

		res += Str( timerStruct.group ) + ";"
			+ Timers.GetKey( pos ) + ";"
			+ Str( timerStruct.delay.count() / 1e6 ) + ";"
			+ Str( timerStruct.delay.count() / 1e6 / timerStruct.count ) + ";"
			+ Str( static_cast<__int64>( timerStruct.count ) ) + ";"
			+ Str( delay * 100 / delayFirstInGroup ) + "%\n";
		pos = Timers.GetNextPosition( pos );
	}

	Timers.Empty();
	return res;
}

