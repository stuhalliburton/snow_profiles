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
  Array.new(10) { |idx| idx == value.to_i-1 ? 1 : 0 }
end

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

    CSV.open(DATA_PATH, "a+") { |csv| csv << new_row }

  rescue NilValueError, NoMethodError, InvalidBearing
    next
  end
end
