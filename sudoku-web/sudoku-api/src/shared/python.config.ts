import { Logger } from '@nestjs/common'
import { Options } from "python-shell"

const logger = new Logger('Python Shell', true);

export const config: Options = {
    mode: 'json',
    pythonPath: '/usr/bin/python3',
    scriptPath: '../../sudoku-solver/',
    pythonOptions: ['-u'],
    stderrParser: (log) => logger.verbose(log)
}
