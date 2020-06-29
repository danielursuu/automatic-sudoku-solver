import { Injectable, Logger } from "@nestjs/common";
import { PythonShell } from "python-shell";
import { Observable, fromEvent } from "rxjs";

import { config } from "./python.config";

@Injectable()
export class RecognizerService {

    private readonly logger = new Logger(RecognizerService.name, true);
    private shell: PythonShell;

    constructor() {
    }

    public startup() {
        this.shell = new PythonShell('sudoku.py', config);
        this.logger.log('RECOGNIZER STARTUP');
    }

    public get Response(): Observable<any> {
        return fromEvent(this.shell, 'message');
    }

    public process(data: any) {
        this.shell.send(data);
    }

    public endShell() {
        this.shell.end((err, code, signal) => {
            if (err) throw err;
            this.logger.log("END SHELL")
        });
    }

}