import { Injectable, Logger } from "@nestjs/common";
import { PythonShell } from "python-shell";
import { config } from "./python.config";
import { Observable, fromEvent } from "rxjs";

@Injectable()
export class PythonService {

    private readonly logger = new Logger(PythonService.name, true);
    private shell: PythonShell;

    constructor() {
    }
    
    public startup() {
        this.shell = new PythonShell('solver.py', config);
        this.logger.log('PYTHON STARTUP');
    }

    public get Response(): Observable<any> {
        return fromEvent(this.shell, 'message');
    }

    public process(data: any) {
        this.shell.send(data);
    }

}