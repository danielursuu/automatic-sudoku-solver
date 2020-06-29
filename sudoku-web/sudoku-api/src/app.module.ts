import { Module } from '@nestjs/common';
import { MulterModule } from '@nestjs/platform-express';

import { AppController } from './app.controller';
import { AppService } from './app.service';
import { SolverService } from './shared/solver.service';
import { DataSolverService } from './shared/data-solver.service';
import { RecognizerService } from './shared/recognizer.service';
import { DataRecognizerService } from './shared/data-recognizer.service';

@Module({
  imports: [MulterModule.register({
    dest: './images'
  })],
  controllers: [AppController],
  providers: [
    AppService,
    SolverService,
    RecognizerService,
    DataSolverService,
    DataRecognizerService
  ],
})
export class AppModule { }
