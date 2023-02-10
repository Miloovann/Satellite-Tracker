#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <netinet/in.h>
#include <stdint.h>


#include <util/log.h>
#include <param/param.h>
#include <csp/csp_cmp.h>




#include <curl/curl.h>

#include <command/command.h>
#include <time.h>

#include "doppler_freq_correction.h"
#include "predict.h"
#include "serial_rotator.h"

/* UHF TXRX frequency carrier freqeuncy */
#define Lumelite_1_TX		435200500
#define Lumelite_1_RX		435200500
#define Lumelite_2_TX		435999500
#define Lumelite_2_RX		435999500
#define Lumelite_3_TX		436800500
#define Lumelite_3_RX		436800500

/* Mapping satellite name to Norad elementid */
#define Lumelite_1		41171 	//e.g. VELOX-II
#define Lumelite_2		41168 	//e.g. ATHENOXAT 1
#define Lumelite_3		41170 	//e.g. GALASSIA 
#define MAX_SAT_SIZE		3	/* Total satellite count */


/* Satellite TLE update*/
//#define CUBESAT_TLE_URL "https://www.celestrak.com/NORAD/elements/cubesat.txt"
#define CUBESAT_TLE_URL ""
#define TLE_LINE_SIZE 		120	/* Length of TLE line */
#define TLE_UPDATE_INTERVAL 	86400	/* Update TLE 24 hrs */
#define DOPPLER_UPDATE_INTERVAL	2	/* Update doppler shift correction interval */
#define TNOW_OFFSET		1200	/* Time offset sec for pre-AOS time tracking*/

/* UHF Ground Station Position*/
/* Reference location: https://inetapps.nus.edu.sg/fas/geog/stationInfo.aspx */
#define LATI 			1.299033
#define LONG 			103.771625
#define ALTI 			50	/* metre */
#define MINI_ELEVATION 		10	/* degree */

void hci_GUI_packet()
{
	log_warning("Initialising doppler shift correction operation...");
	
	/* Get current time in CSP_timestamp*/
	csp_timestamp_t clock;
	clock_get_time(&clock);
	uint32_t Tnow = clock.tv_sec;

	/*Set latitude, longitude and altitude for the UHF ground station */
	setStation(LATI, LONG, ALTI);

	/* Update TLE for the target satellite.  */
        int sat_no = 1;
	mcs_sat_sel(sat_no); 
	
	long Time_aos_prev = 0;

	while (1)
	{			
		/* Estimate next ground pass AOS and LOS time*/
		set_calc_time(Tnow - (TNOW_OFFSET));
		PreCalc();
		Calc();

		/* Find time for begin and end of pass */
		long Time_aos = floor(86400.0 * (3651.0 + NextAOS()));
		long Time_los = floor(86400.0 * (3651.0 + FindLOS2()));

		/* Find AZ at AOS */
		set_calc_time(Time_aos);
		PreCalc();
		Calc();
		int Azi_aos = get_azi();

		/* Find AZ at LOS */
		set_calc_time(Time_los);
		PreCalc();
		Calc();
		int Azi_los = get_azi();
		
		/* Find Max Elevation */
		long Time_maxele = (Time_aos+Time_los)/2;
		set_calc_time(Time_maxele);
		PreCalc();
		Calc();
		int Azi_m = get_azi();
		int Ele_m = get_ele();
		if(Time_aos != Time_aos_prev)
		{
			log_info("AOS: %.24s %lu @ %u deg azimuth", ctime((time_t *) &Time_aos), Time_aos, Azi_aos);
			log_info("LOS: %.24s %lu @ %u deg azimuth", ctime((time_t *) &Time_los), Time_los, Azi_los);
			log_info("Max Elevation: %u deg elevation %u deg azimuth @ %.24s", Ele_m, Azi_m, ctime((time_t *) &Time_maxele));
		
			log_warning("Ground pass initialisation done.");

			/* Convert log_info into a char string for storage */
			char HCI_buffer[128] = {0};
			memset(HCI_buffer,0,sizeof HCI_buffer); // Clear buffer
			sprintf(HCI_buffer, "AOS: %.24s %lu @ %u deg azimuth\nLOS: %.24s %lu @ %u deg azimuth\nMax Elevation: %u deg elevation %u deg azimuth @ %.24s", ctime((time_t *) &Time_aos), Time_aos, Azi_aos, ctime((time_t *) &Time_los), Time_los, Azi_los, Ele_m, Azi_m, ctime((time_t *) &Time_maxele));
			
			FILE * hci_fp;
                        hci_fp = fopen("test.txt","rb+");
                        fprintf(hci_fp, "%s\n", HCI_buffer);

                        fclose(hci_fp);
                        
                        
                        printf("\n%lu\n%s\n", Tnow, HCI_buffer);

	       
			/* Determine if ground pass is skipped: min elevation */
			log_debug("Preparing for next ground pass ...")
		}

		Time_aos_prev = Time_aos;
		sleep(1);
		ground_pass_in_progress(Time_aos,Time_los);

		/* Update tnow */
		clock_get_time(&clock);
		Tnow = clock.tv_sec;

		
		//long tnowl = tnow;
		//log_debug("Current time: %.24s", ctime((time_t *) &tnowl));
		//log_debug("Next LOS: %.24s", ctime((time_t *) &time_los));
		//log_info("Current satellite number: %u", sat_no)

		/* Auto increment sat_no to track for next ground pass*/
		if ( (Tnow) > Time_los)
		{
			if( (sat_no + 1) <= MAX_SAT_SIZE )
				sat_no += 1;
			else
				sat_no = 1;
			log_debug("Tracking Satellite No. %d in next ground pass", sat_no)
			mcs_sat_sel(sat_no);
		}
		/* Check if MCS update sat_no */
		// check sat_select file, if len() != 0 or sat_no != sat
	}
	
	return;	
}

