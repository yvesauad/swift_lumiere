from nion.swift.model import HardwareSource
import numpy
import time
from nion.typeshed import API_1_0 as API
from nion.typeshed import UI_1_0 as UI
from nion.utils import Geometry

api = api_broker.get_api(API.version, UI.version)

scan = HardwareSource.HardwareSourceManager().get_hardware_source_for_hardware_source_id("usim_scan_device")
stage = HardwareSource.HardwareSourceManager().get_instrument_by_id("stage_controller")
my_inst = HardwareSource.HardwareSourceManager().get_instrument_by_id("usim_stem_controller")

print(my_inst.GetVal2D("stage_position_m"))
pos = Geometry.FloatPoint(y=1e-9, x=1e-8)
my_inst.SetVal2D("stage_position_m", pos)

xdata = numpy.random.randn(10, 10, 1024)
intensity_calibration = api.create_calibration(offset=0.0, scale=4.0, units='counts')
dimensional_calibration_0 = api.create_calibration(0.0, 10, '0U')
dimensional_calibration_1 = api.create_calibration(0.0, 20, '1U')
dimensional_calibration_2 = api.create_calibration(0.0, 30, '2U')
dimensional_calibrations = [dimensional_calibration_0, dimensional_calibration_1, dimensional_calibration_2]
si_data_descriptor = api.create_data_descriptor(is_sequence=False, collection_dimension_count=2, datum_dimension_count=1)
si_xdata = api.create_data_and_metadata(xdata, data_descriptor=si_data_descriptor,
                                        intensity_calibration=intensity_calibration,
                                        dimensional_calibrations=dimensional_calibrations)
data_item = api.library.create_data_item_from_data_and_metadata(si_xdata)

oi

det = scan.grab_next_to_start()[0]
data_item = api.library.create_data_item_from_data_and_metadata(det)
print(dir(data_item))
data_item.title = 'First Image'

pts = 16
sub_region = 0.25

xarray = numpy.linspace(-sub_region, sub_region, pts)
yarray = numpy.linspace(-sub_region, sub_region, pts)

fov = scan.scan_device.field_of_view
ia = scan.scan_device.Image_area

x_samp = (fov*1e9)/(ia[3]-ia[2])
y_samp = (fov*1e9)/(ia[5]-ia[4])

initial_stage_x = stage.x_pos_f
initial_stage_y = stage.y_pos_f

initial_probe_x = scan.scan_device.probe_pos[0]
initial_probe_y = scan.scan_device.probe_pos[1]

initial_probe_pixel = scan.scan_device._Device__probe_position_pixels

if abs(initial_probe_x-0.5)>0.01 or abs(initial_probe_y-0.5)>0.01:
    raise Exception("***MECHANICAL SPECTRA***: Put probe close to (0.5, 0.5). 1% tolerance allowed. ")

print(((ia[3]-ia[2])/pts).is_integer())

if not ((ia[3]-ia[2])/pts).is_integer() or not ((ia[5]-ia[4])/pts).is_integer():
    raise Exception("***MECHANICAL SPECTRA***: Number of points (pts) is not a divisor of image area (in pixels)")

print(f'Probe Sampling Precision (nm): {x_samp} nm and {y_samp} nm.')
print(f'Mechanical step is (nm): {(fov*1e9)/pts} and {(fov*1e9)/pts}')
print(f'Image area (pixels): {(ia[3]-ia[2])} and {(ia[5]-ia[4])}')
print(f'Pixels per step: {(ia[3]-ia[2])/pts} and {(ia[5]-ia[4])/pts}')
print(f'initial probe position is {initial_probe_x} and {initial_probe_y}')
print(f'initial probe position (in pixels) is {initial_probe_pixel}')

stage.x_pos_f = initial_stage_x - sub_region*fov*1e8 #You put 400 to have 4 microns in this property here
stage.y_pos_f = initial_stage_y - sub_region*fov*1e8
cam_eire.start_playing()
data = list()
xdata = numpy.zeros((pts, pts, 1600))
time.sleep(0.25)

sen = -1
for xi, x in enumerate(xarray):
    stage.x_pos_f = initial_stage_x + x*fov*1e8 #You put 400 to have 4 microns in this property here
    sen = sen * -1
    for yi, y in enumerate(yarray):
        for val in my_inst._ivgInstrument__stage_moving:
            if val:
                raise Exception("***MECHANICAL SPECTRA***: Motor move during a new command.")
        stage.y_pos_f = initial_stage_y + y*fov*1e8*sen
        data = cam_eire.grab_next_to_finish()
        data.append([stage.x_pos_f, stage.y_pos_f, data[0]])
        xdata[xi, yi] = data[0].data
        #scan.scan_device.probe_pos = ((x+0.5), (y+0.5))

si_data_descriptor = api.create_data_descriptor(is_sequence=False, collection_dimension_count=2, datum_dimension_count=1)
si_xdata = api.create_data_and_metadata(xdata, data_descriptor=si_data_descriptor)
data_item = api.library.create_data_item_from_data_and_metadata(si_xdata)

stage.x_pos_f = initial_stage_x
stage.y_pos_f = initial_stage_y
cam_eire.stop_playing()
#scan.scan_device.probe_pos = (initial_probe_x, initial_probe_y)
