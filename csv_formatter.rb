require 'csv'

CSV_DIR = './profiles'
RELEVENT_COLUMNS = [
  ' Grid',
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
  ' Avalanche Code',
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
  'Considerable +' => 3
}
NUMBERS_REGEX = /(\-?\d+\.?\d*)/
DATA_PATH = './data/parsed.csv'
WRITE_HEADERS = [*RELEVENT_COLUMNS, 'Forecast aval. hazard', 'Observed aval. hazard'].map { |header| header.strip }


CSV.open(DATA_PATH, 'w') { |writer| writer << WRITE_HEADERS }

class NilValueError < StandardError; end

Dir.glob(CSV_DIR + '/**/*.csv').each do |csv_path|
  CSV.foreach(csv_path, headers: true) do |row|
    new_row = []

    RELEVENT_COLUMNS.each do |column_name|
      raise NilValueError if row[column_name].empty?
      value = NUMBERS_REGEX.match(row[column_name])[0]
      new_row << value
    end
    new_row << RISK_LABELS[row[' Forecast aval. hazard']]
    new_row << RISK_LABELS[row[' Observed aval. hazard']]

    CSV.open(DATA_PATH, "a+") { |csv| csv << new_row }

  rescue NilValueError
    next
  end
end
