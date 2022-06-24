def upsertORACLESData(this):
    """
    Function to Open files in the ObservationOutputFile table and then populate ObservationOutput data.
    
    - Arguments:
        -this: an instance of ObservationOutputFile
    - Returns:
        -bool: True if file was processed, false if file has already been processed
    """
    from datetime import datetime
    import pandas as pd

    class ObsVars:
        nc_variables = ['time', 'Longitude', 'Latitude', 'GPS_Altitude', 
                        'rBC_massConc', 'Static_Air_Temp', 'Static_Pressure','Dew_Point','Lambda_Avg_SSA_Front',
                        'Lambda_Avg_SSA_Rear', 'TSI_Scat530', 'NO3', 'SO4', 'ORG',
                        'CNgt10', 'Chl', 'UHSASdNdlogd']
        
        #Check the other ATom data file for additional variables
        
        nc_variables_atom = ['time', 'Wavelength', 'Diameter', 'lognorm_params', 
                        'gps_altitude', 'latitude', 'longitude','ambient_pressure','ambient_temperature',
                        'RHw_DLH', 'theta', 'ozone', 'CO', 'num_fine',
                        'sfc_fine', 'vol_fine', 'num_coarse', 'sfc_coarse', 'vol_coarse', 'num_nucl',
                        'sfc_nucl', 'vol_nucl', 'num_Aitken', 'sfc_Aitken', 'vol_Aitken', 'num_accum',
                        'sfc_accum', 'vol_accum', 'dndlogd', 'sulf_org_dndlogd', 'dust_dndlogd',
                        'BB_dndlogd', 'SS_dndlogd', 'alk_dndlogd', 'meteoritic_dndlogd', 'EC_dndlogd',
                        'comb_dndlogd', 'dndlogd_ambRH', 'sulf_org_dndlogd_ambRH', 'dust_dndlogd_ambRH',
                        'BB_dndlogd_ambRH', 'SS_dndlogd_ambRH', 'alk_dndlogd_ambRH', 'meteoritic_dndlogd_ambRH' #not needed
                        ,'EC_dndlogd_ambRH', 'comb_dndlogd_ambRH', 'sulfate_calc', 'nitrate_calc',
                        'ammonium_calc', 'chl_calc', 'oa_calc', 'ext_dry_ambPT', 'ext_ambRHPT', 
                        'BC_abs_ambPT', 'BrC_abs_ambPT', 'scat_dry_ambPT', 'scat_ambRHPT',
                        'backscat_ambRHPT', 'asymmetry_dry', 'asymmetry_amRH', 'ext_Angstrom_dry',
                        'ext_angstrom_ambRH', 'ext_angstrom_ambRH', 'ext_angstrom_ambRH_uv_vis', 
                        'ext_Angstrom_dry_vis_ir', 'ext_angstrom_ambRH_vis_ir', 'abs_Angstrom_UV_Vis',
                        'abs_Angstrom_Vis_IR', 'MEE_dry', 'MEE_ambRH', 'ext_backscat_ratio_ambRH',
                        'backscatt_eff_ambRH', 'SSA_dry', 'SSA_ambRH', 'lognorm_coefs_nucl', 
                        'lognorm_coefs_Aitken', 'lognorm_coefs_accum', 'lognorm_coefs_coarse',
                        'CCN_005', 'CCN_010', 'CCN_020', 'CCN_050', 'CCN_100', 'f_rh_85',
                        'f_rh_85_fit', 'kappa_ext', 'kappa_ams']
    
        variables_map = {'time':'start', 
                'Longitude':'longitude', 
                'Latitude':'latitude', 
                'GPS_Altitude':'altitude',
                'rBC_massConc':'total_BC', 
                'Static_Air_Temp':'temperature', 
                'Static_Pressure':'pressure', 
                'Dew_Point':'dewpoint', 
                'Lambda_Avg_SSA_Front':'SSA_front', 
                'Lambda_Avg_SSA_Rear':'SSA_rear', 
                'TSI_Scat530':'scat530', 
                'NO3':'NO3', 
                'SO4':'total_SO4', 
                'ORG':'total_ORG', 
                'CNgt10':'CNgt10', 
                'Chl':'total_Cl', 
                'UHSASdNdlogd':'UHSASdNdlogd'}
        
        variables_map_atom = {'time':'start', #units: seconds since 1904-01-01 00:00:00
                'longitude':'longitude', #units: degrees_east
                'latitude':'latitude', #units: degrees_north
                'gps_altitude':'altitude', #units: meters
                ' ':'total_BC', #???
                'ambient_temperature':'temperature', #units: K at ambient
                'ambient_pressure':'pressure', #units: hPa at ambient
                'Dew_Point':'dewpoint', #???
                'Lambda_Avg_SSA_Front':'SSA_front', #??? 'SSA_dry single_scatter_albedo_dry
                'Lambda_Avg_SSA_Rear':'SSA_rear', #??? 'SSA_ambRH' single_scatter_albedo_ambient_RH
                'TSI_Scat530':'scat530', #???
                'NO3':'NO3', #???
                'SO4':'total_SO4', #??? sulfate_calc
                'ORG':'total_ORG', #???
                'CNgt10':'CNgt10', #Source is not implicit ???
                'chl_calc':'total_Cl', #units: ug_cm^-3
                'UHSASdNdlogd':'UHSASdNdlogd' #unknowns??? }

        def get_df_from_c3_file(c3file):
            """
            Opens file, grab variables in the variables_map and returns pandas DataFrame
            """
            source = c3.NetCDFUtil.openFile(c3file.file.url)
            df = pd.DataFrame()
    
            for nc_var in ObsVars.nc_variables:
                c3_var = ObsVars.variables_map[nc_var]
                if nc_var == 'time':
                    df[c3_var] = source.variables[nc_var][:]
                    df[c3_var] = pd.to_datetime(df[c3_var],unit='s')
                elif nc_var == 'UHSASdNdlogd':
                    for i in range(0,1):
                        name = c3_var + "_bin" + str(i)
                        try:
                            df[name] = source.variables[nc_var][:,i]
                        except:
                            pass
                else:
                    try:
                        df[c3_var] = source.variables[nc_var][:]
                    except:
                        pass
            return df

    df = ObsVars.get_df_from_c3_file(this)
    obsSet = c3.ObservationSet.get(this.observationSet.id)
    parent_id = "OOS_SetName_" + obsSet.name + "_Ver_" + obsSet.versionTag
    df['parent'] = parent_id

    zero_time = datetime(1970,1,1,0,0)
    now_time = datetime.now()
    diff_time = (now_time - zero_time)
    versionTag= -1 * diff_time.total_seconds()
    df['dataVersion'] = versionTag

    output_records = df.to_dict(orient="records")

    # upsert this batch
    c3.ObservationOutput.upsertBatch(objs=output_records)

    this.processed = True
    c3.ObservationOutputFile.merge(this)
    return True