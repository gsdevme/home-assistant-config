### Changes

v3.0.45
- pre release
- currently being tested 
- wont hurt anything if you do install it

v3.0.44
- pre release
- better diagnotic data
- just for testing
- wont hurt anything if you do install it

v3.0.43
- pre release not for use!!
- do not install :) just for testing

v3.0.42
- fixed using the service to update forecasts from calling twice

v3.0.41
- recoded logging. Re-worded. More debug vs info vs error logging.
- API usage counter was not recorded when reset to zero at UTC midnight
- added a new service where you can call to update the Solcast Actuals data for the forecasts
- added the version info to the intergation UI

v3.0.40
- someone left some unused code in 3.0.39 causing problems

v3.0.39
- removed version info

v3.0.38
- error with v3.0.37 fix for updating sensors

v3.0.37
- make sure the hourly sensors update when auto polling is disabled

v3.0.36
- includes all pre release items
- actual past accurate data is now set to only poll the API at midday and last hour of the day (so only twice a day)

v3.0.35 - PRE RELEASE
- extended the internet connection timeout to 60s

v3.0.34 - PRE RELEASE
- added service to clear old solcast.json file to have a clean start
- return empty energy graph data if there is an error generating info

v3.0.33
- added sensors for forecast days 3,4,5,6,7

v3.0.32
- refactored HA setup function call requirements
- refactored some other code with typos to spell words correctly.. no biggie

v3.0.30
- merged in some work by @696GrocuttT PR into this release
- fixed code to do with using up all allowed api counts
- this release will most likely stuff up the current API counter, but after the UTC counter reset all will be right in the world of api counting again

v3.0.29
- changed Peak Time Today/Tomorrow sensor from datetime to time
- changed back the unit for peak measurement to Wh as the sensor is telling the peak/max hours generated forecast for the hour
- added new configuration option for the integration to disable auto polling. Users can then setup their own automation to poll for data when they like (mostly due to the fact that Solcast have changed the API allowance for new accounts to just 10 per day)
- API counter sensor now shows total used instead of allowance remaining as some have 10 others 50. It will 'Exceeded API Allowance' if you have none left


v3.0.27
- changed unit for peak measurement #86 tbanks Ivesvdf
- some other minor text changes for logs
- changed service call thanks 696GrocuttT
- including fix for issue #83

v3.0.26
- testing fix for issue #83

v3.0.25
- removed PR for 3.0.24 - caused errors in the forecast graph
- fixed HA 2022.11 cant add forcast to solar dashboard

v3.0.24
- merged PR from @696GrocuttT 

v3.0.23
- added more debug log code
- added the service to update forecast

v3.0.22
- added more debug log code

v3.0.21
- added more debug logs for greater info

v3.0.19
- FIX: coordinator.py", line 133, in update_forecast for update_callback in self._listeners: RuntimeError: dictionary changed size during iteration
- this version needs HA 2022.7+ now

v3.0.18
- changed api counter return value calculations

v3.0.17
- set the polling api time to 10mins after the hour to give solcast api time to calculate satellite data

v3.0.16
- fixed api polling to get actual data once in a while during the day
- added full path to data file - thanks OmenWild

v3.0.15
- works in both 2022.6 and 2022.7 beta

v3.0.14
- fixes HA 2022.7.0b2 errors (seems to :) )

v3.0.13
- past graphed data did not reset at midnight local time
- missing asyncio import

v3.0.12
- graphed data for week/month/year was not ordered so the graph was messy

v3.0.11
- added timeout for solcast api server connections
- added previous 7 day graph data to the energy dashboard (only works if you are recording data)

v3.0.9
- **users upgrading from v3.0.5 or lover, need to delete the 'solcast.json' file in the HA>config directory to stop any errors**
- renamed sensors with the prefix "solcast_" to help naming sensors easier
- ** you will get double ups of the sensors in the integration because of the naming change. these will show greyed out in the list or with the values like unknown or unavailable etc.. just delete these old sensors one by one from the integration **

v3.0.6
- **users upgrading from v3.0.x need to delete the 'solcast.json' file in the HA>config directory**
- fixed lots of little bugs and problems.
- added ability to add multiple solcast accounts. Just comma seperate the api_keys in the integration config.
- remained API Counter to API Left. shows how many is remaining rather than used count.
- 'actual forecast' data is now only called once, the last api call at sunset. OR during integration install first run.
- forecast data is still called every hour between sunrise and sunset and once at midnight every day.
*Just delete the old API Counter sensor as its not used now*

v3.0.5 beta
- fixed 'this hour' amd 'next hour' sensor values.
- slow down the api polling if more than 1 rooftop to poll.
- fix first hour graph plot data.
- possibly RC1?? will see.

v3.0.4 beta
- bug fixes.

Complete re write. v3.0 now 
**Do not update this if you like the way the older version worked**
*There are many changes to this integration*

Simple setup.. just need the API key

- This is now as it should be, a 'forecast' integration (it does not graph past data *currently*)
- Forecast includes sensors for "today" and "tomorrow" total production, max hour production and time.. this hour and next production
- Forecast graph info for the next 7 days of data available

Integration contains
  - API Counter             (int)
  - API Last Polled         (date/time)
  - Forecast Next Hour      (Wh)
  - Forecast This Hour      (Wh)
  - Forecast Today          (kWh) (Attributes calculated from 'pv_estimate')
  - Forecast Tomorrow       (kWh) (Attributes calculated from 'pv_estimate')
  - Peak Forecast Today     (Wh)
  - Peak Forecast Tomorrow  (Wh)
  - Peak Time Today         (date/time)
  - Peak Time Tomorrow      (date/time)

![demo](https://user-images.githubusercontent.com/1471841/172541966-cb3f84a9-66bd-4f0f-99de-6d3e52cfd2ba.png)



### Polling Imformation
Solcast has a 50 API poll limit per day.

