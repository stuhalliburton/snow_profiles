require 'csv'
require 'fileutils'

CSV_DIR = './profiles'
RELEVENT_COLUMNS = [
#  ' Grid',
  ' Alt',
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
  ' Snow Index',
  ' Insolation',
  ' Crystals',
  ' Wetness',
  ' AV Cat',
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
DATA_PATH = './data/parsed.csv'

class NilValueError < StandardError; end

FileUtils.rm(DATA_PATH) if File.exists?(DATA_PATH)

Dir.glob(CSV_DIR + '/**/*.csv').each do |csv_path|
  CSV.foreach(csv_path, headers: true) do |row|
    new_row = []

    RELEVENT_COLUMNS.each do |column_name|
      raise NilValueError if row[column_name].empty?
      value = NUMBERS_REGEX.match(row[column_name])[0]
      new_row << value
    end

#    next if RISK_LABELS[row[' Forecast aval. hazard']].nil?
#    new_row << RISK_LABELS[row[' Forecast aval. hazard']]
    next if RISK_LABELS[row[' Observed aval. hazard']].nil?
    new_row << RISK_LABELS[row[' Observed aval. hazard']]

    CSV.open(DATA_PATH, "a+") { |csv| csv << new_row }

  rescue NilValueError, NoMethodError
    next
  end
end
