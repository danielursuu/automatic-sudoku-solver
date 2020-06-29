import { Injectable, Logger } from "@nestjs/common";
import { Subject, Observable } from "rxjs";
import { PythonService } from "./python.service";

@Injectable()
export class DataService {

    private readonly logger = new Logger(DataService.name, true);

    private queue: any[] = [];
    private ready = false;
    private output: Subject<any> = new Subject<any>();

    constructor(
        private readonly pythonService: PythonService
    ) {

    }

    public start() {
        this.pythonService.startup();
        this.pythonService.Response.subscribe((data) => {
            this.output.next(data);
        });
    }

    public input(input) {
        this.queue.push(input);
        if (this.ready) {
            this.process();
        }
    }

    private process(): void {
        if (this.queue.length !== 0) {
            this.ready = false;
            this.pythonService.process(this.queue.shift())
        }
    }

    public get Output(): Observable<any> {
        return this.output;
    }
}