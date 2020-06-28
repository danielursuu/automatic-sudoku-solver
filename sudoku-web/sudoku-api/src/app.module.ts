import { Module } from '@nestjs/common';
import { MulterModule } from '@nestjs/platform-express';

import { AppController } from './app.controller';
import { AppService } from './app.service';
import { PythonService } from './shared/python.service';
import { DataService } from './shared/data.service';

@Module({
  imports: [MulterModule.register({
    dest: './images'
  })],
  controllers: [AppController],
  providers: [
    AppService,
    PythonService,
    DataService
  ],
})
export class AppModule { }
