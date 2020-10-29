#pragma once

#include <chrono>
#include <map>
#include <vector>
#include <sstream>
#include <mutex>
#include <iomanip>

using namespace std::chrono;

class CTimer {
public:
	CTimer( bool start = false ) : CTimer( "", "", start ) {}

	CTimer( const char* _name, std::string _groupName = "", bool start = false )
			: name( _name ), groupName( _groupName ), timeDelay( 0 ), count(0), isStarted( false ) {
		if( start ) {
			Start();
		}
	}
	~CTimer() {
		if( isStarted ) {
			Stop();
		}
		if( !name.empty() ) {
			const std::lock_guard<std::mutex> lock( TimersGuard );
			auto& timer = Timers[name];
			timer.delay += timeDelay;
			timer.count += count;
			timer.group = groupName;
		}
	}

	void Start() {
		assert( !isStarted );
		startTime = high_resolution_clock::now();
		isStarted = true;
	}
	void Stop() {
		assert( isStarted );
		auto stopTime = high_resolution_clock::now();
		timeDelay += duration_cast<nanoseconds>( stopTime - startTime );
		count++;
		isStarted = false;
	}

	float GetTimeInMs() const {
		auto currentTime = isStarted ? high_resolution_clock::now() - startTime : timeDelay;
		return currentTime.count() / 1e6;
	}

	static string PrintTimers() {
		if( Timers.empty() ) return "";

		using namespace std;
		const std::lock_guard<std::mutex> lock( TimersGuard );
		stringstream ss;
		ss << endl
			<< setw( 10 ) << left << "Group"
			<< setw( 30 ) << "Timer name"
			<< setw( 20 ) << "Total, ms"
			<< setw( 20 ) << "Avrg, ms"
			<< setw( 8 ) << "Count"
			<< setw( 10 ) << right << "%" << endl;

		vector<pair<string, CTimerStruct>> timers;
		for( auto& timer : Timers ) {
			timers.push_back( timer );
		}
		sort( timers.begin(), timers.end(),
			[]( pair<string, CTimerStruct>& a, pair<string, CTimerStruct>& b ) {
				return a.second.group < b.second.group || a.second.group == a.first;
			} );

		for( auto& timer : timers ) {
			auto& timerStruct = timer.second;
			double delay = static_cast<double>( timerStruct.delay.count() ) / 1e6;
			// a head timer is a timer with the name equivalent to the group name
			auto groupHead = Timers.find( timerStruct.group );
			double delayFirstInGroup = static_cast<double>( 
				groupHead == Timers.end() ? delay : groupHead->second.delay.count() / 1e6 );

			ss << setw( 8 ) << left << timerStruct.group
				<< setw( 30 ) << timer.first
				<< setw( 20 ) << timerStruct.delay.count() / 1000000
				<< setw( 20 ) << setprecision(3) << timerStruct.delay.count() / 1e6 / timerStruct.count
				<< setw( 8 ) << fixed << timerStruct.count 
				<< setw( 10 ) << right << delay * 100 / delayFirstInGroup << "%" << endl;
		}
		Timers.clear();
		return ss.str();
	}

private:
	struct CTimerStruct {
		CTimerStruct() : delay( 0 ), count ( 0 ) {}

		nanoseconds delay;
		int64_t count;
		std::string group;
	};

	std::string name;
	std::string groupName;
	system_clock::time_point startTime;
	nanoseconds timeDelay;
	int64_t count;
	bool isStarted;
	static std::map<std::string, CTimerStruct> Timers;
	static std::mutex TimersGuard;
};

