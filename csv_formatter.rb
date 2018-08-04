require 'csv'
require 'fileutils'

class NilValueError < StandardError; end
class InvalidBearing < StandardError; end
class InvalidPrecipCode < StandardError; end

CSV_DIR = './profiles'
RELEVENT_COLUMNS = [
#  ' Grid',
#  ' Alt',
  ' Aspect',
  ' Incline',
  ' Air Temp',
  ' Wind Dir',
  ' Wind Speed',
  ' Cloud',
  ' Precip Code',
  ' Drift',
  ' Total Snow Depth',
  ' Foot Pen',
  ' Ski Pen',
  ' Rain at 900',
  ' Summit Air Temp',
  ' Summit Wind Dir',
  ' Summit Wind Speed',
#  ' Avalanche Code',
  ' Max Temp Grad',
  ' Max Hardness Grad',
  ' No Settle',
#  ' Snow Index',
  ' Insolation',
  ' Crystals',
  ' Wetness',
#  ' AV Cat',
  ' Snow Temp'
  # ' Forecast aval. hazard',
  # ' Observed aval. hazard',
]
RISK_LABELS = {
  'Low' => 0,
  'Moderate' => 1,
  'Considerable -' => 2,
  'Considerable +' => 3,
  'High' => 4
}
NUMBERS_REGEX = /(\-?\d+\.?\d*)/
BEARING_REGEX = /Dir$|Aspect$/
PRECIP_REGEX = /Precip Code$/

DATA_PATH = './data/parsed.csv'

FileUtils.rm(DATA_PATH) if File.exists?(DATA_PATH)


def encode_bearing(value)
  case value.to_f
  when (337.6..360) || (0..22.5)
    [1, 0, 0, 0, 0, 0, 0, 0]
  when 22.6..67.5
    [0, 1, 0, 0, 0, 0, 0, 0]
  when 67.6..112.5
    [0, 0, 1, 0, 0, 0, 0, 0]
  when 112.6..157.5
    [0, 0, 0, 1, 0, 0, 0, 0]
  when 157.6..202.5
    [0, 0, 0, 0, 1, 0, 0, 0]
  when 202.5..247.5
    [0, 0, 0, 0, 0, 1, 0, 0]
  when 247.6..292.5
    [0, 0, 0, 0, 0, 0, 1, 0]
  when 292.6..337.5
    [0, 0, 0, 0, 0, 0, 0, 1]
  else
    raise InvalidBearing
  end
end

def encode_precip_code(value)
  case value.to_i
  when 0 then [1, 0, 0, 0, 0, 0]
  when 2 then [0, 1, 0, 0, 0, 0]
  when 4 then [0, 0, 1, 0, 0, 0]
  when 6 then [0, 0, 0, 1, 0, 0]
  when 8 then [0, 0, 0, 0, 1, 0]
  when 10 then [0, 0, 0, 0, 0, 1]
  else
    raise InvalidPrecipCode
  end
end

def csv_headers
  [
    'aspect_n',
    'aspect_ne',
    'aspect_e',
    'aspect_se',
    'aspect_s',
    'aspect_sw',
    'aspect_w',
    'aspect_nw',
    'incline',
    'air_temp',
    'wind_dir_n',
    'wind_dir_ne',
    'wind_dir_e',
    'wind_dir_se',
    'wind_dir_s',
    'wind_dir_sw',
    'wind_dir_w',
    'wind_dir_nw',
    'wind_speed',
    'cloud',
    'precip_code_0',
    'precip_code_2',
    'precip_code_4',
    'precip_code_6',
    'precip_code_8',
    'precip_code_10',
    'drift',
    'total_snow_depth',
    'foot_pen',
    'ski_pen',
    'rain_at_900',
    'summit_air_temp',
    'summit_wind_dir_n',
    'summit_wind_dir_ne',
    'summit_wind_dir_e',
    'summit_wind_dir_se',
    'summit_wind_dir_s',
    'summit_wind_dir_sw',
    'summit_wind_dir_w',
    'summit_wind_dir_nw',
    'summit_wind_speed',
    'max_temp_grad',
    'max_hardness_grad',
    'no_settle',
    'insolation',
    'crystals',
    'wetness',
    'snow_temp',
    'hazard_rating'
  ]
end

CSV.open(DATA_PATH, "w", write_headers: true, headers: csv_headers) do |csv|
  Dir.glob(CSV_DIR + '/**/*.csv').each do |csv_path|
    CSV.foreach(csv_path, headers: true) do |row|
      new_row = []

      RELEVENT_COLUMNS.each do |column_name|
        raise NilValueError if row[column_name].empty?
        value = NUMBERS_REGEX.match(row[column_name])[0]

        value = encode_bearing(value) if BEARING_REGEX.match(column_name)
        value = encode_precip_code(value) if PRECIP_REGEX.match(column_name)

        new_row << value
      end

      # next if RISK_LABELS[row[' Forecast aval. hazard']].nil?
      # new_row << RISK_LABELS[row[' Forecast aval. hazard']]
      next if row[' Observed aval. hazard'].empty?
      new_row << RISK_LABELS.fetch(row[' Observed aval. hazard'])
      new_row.flatten!

      csv << new_row

    rescue NilValueError, NoMethodError, InvalidBearing
      next
    end
  end
end
